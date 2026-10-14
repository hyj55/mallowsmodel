// Exact lexicographic greedy Kendall packing, without factorial-size arrays.
// This executable only constructs the packing; it never accepts observed ranks
// or changes pair extraction, radius, objective, or estimator tie-breaking.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <memory>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
#include <deque>
#include <cstdio>
#include <sys/resource.h>

using Clock = std::chrono::steady_clock;

// Move past EVERY permutation with the current prefix of length length.
// No lexicographic integer ranks are needed, even when n! exceeds uint64.
bool advance_prefix(std::vector<unsigned>& p, unsigned length) {
    std::vector<bool> available(p.size(), true);
    for (unsigned i=0; i<length; ++i) available[p[i]]=false;
    for (int i=int(length)-1; i>=0; --i) {
        available[p[i]]=true;
        for (unsigned x=p[i]+1; x<p.size(); ++x) if (available[x]) {
            p[i]=x; available[x]=false;
            unsigned j=unsigned(i)+1;
            for (unsigned y=0; y<p.size(); ++y) if (available[y]) p[j++]=y;
            return true;
        }
    }
    return false;
}

template<class Label> class Packing {
    static constexpr size_t block_size=256;
    struct Chunk {
        std::unique_ptr<uint64_t[]> bits;
        std::unique_ptr<Label[]> ranks;
        Chunk(unsigned n,unsigned words):bits(new uint64_t[block_size*words]),
            ranks(new Label[block_size*n]) {}
    };
    unsigned n,words;
    size_t budget,base_block=0,resident_limit,block_bytes;
    std::deque<std::unique_ptr<Chunk>> resident;
    mutable std::unique_ptr<Chunk> scratch;
    mutable size_t scratch_block=std::numeric_limits<size_t>::max();
    std::string spill_path;
    mutable std::fstream spill;
    size_t reserve() const {return (2<<20)+16*size_t(words)+64*size_t(n);}
    const Chunk& chunk(size_t block) const {
        if (block>=base_block) return *resident.at(block-base_block);
        if (scratch_block!=block) {
            if (!scratch) scratch=std::make_unique<Chunk>(n,words);
            spill.seekg(std::streamoff(block*block_bytes));
            spill.read(reinterpret_cast<char*>(scratch->bits.get()),block_size*words*8);
            spill.read(reinterpret_cast<char*>(scratch->ranks.get()),block_size*n*sizeof(Label));
            if (!spill) throw std::runtime_error("Cannot read spilled candidate block");
            scratch_block=block;++disk_reads;
        }
        return *scratch;
    }
public:
    size_t count=0,disk_writes=0;
    mutable size_t disk_reads=0;
    Packing(unsigned size,size_t limit,const std::string& prefix):n(size),
        words((size*(size-1)/2+63)/64),budget(limit),
        block_bytes(block_size*(8*size_t(words)+sizeof(Label)*n)),
        spill_path(prefix+".index"),
        spill(spill_path,std::ios::binary|std::ios::in|std::ios::out|std::ios::trunc) {
        if (!spill) throw std::runtime_error("Cannot open temporary candidate index");
        // Keep one reusable read buffer in reserve. All older blocks live on
        // disk; no in-memory directory grows with the number of spilled blocks.
        size_t slots=budget>reserve()?(budget-reserve())/block_bytes:0;
        resident_limit=slots>1?slots-1:0;
    }
    ~Packing() {spill.close();std::remove(spill_path.c_str());}
    size_t allocated() const {
        return reserve()+(resident.size()+size_t(bool(scratch)))*block_bytes;
    }
    bool append(const std::vector<unsigned>& p,const std::vector<uint64_t>& b) {
        if (!resident_limit) return false;
        if (count%block_size==0) {
            if (resident.size()==resident_limit) {
                if (base_block>size_t(std::numeric_limits<std::streamoff>::max())/block_bytes)
                    throw std::runtime_error("Candidate index exceeds file offset representation");
                spill.seekp(std::streamoff(base_block*block_bytes));
                spill.write(reinterpret_cast<const char*>(resident.front()->bits.get()),block_size*words*8);
                spill.write(reinterpret_cast<const char*>(resident.front()->ranks.get()),block_size*n*sizeof(Label));
                spill.flush();
                if (!spill) throw std::runtime_error("Cannot write spilled candidate block");
                resident.pop_front();++base_block;++disk_writes;
            }
            resident.push_back(std::make_unique<Chunk>(n,words));
        }
        auto& c=*resident.back();size_t row=count%block_size;
        std::copy(b.begin(),b.end(),c.bits.get()+row*words);
        for (unsigned i=0;i<n;++i) c.ranks[row*n+p[i]]=Label(i);
        ++count;return true;
    }
    const Label* rank(size_t index) const {
        return chunk(index/block_size).ranks.get()+(index%block_size)*n;
    }
    size_t covering(const std::vector<uint64_t>& b,unsigned radius,uint64_t& comparisons) const {
        for (size_t ix=count;ix>0;--ix) {
            auto ref=chunk((ix-1)/block_size).bits.get()+((ix-1)%block_size)*words;
            unsigned distance=0;++comparisons;
            for (unsigned w=0;w<words && distance<=radius;++w)
                distance+=unsigned(__builtin_popcountll(b[w]^ref[w]));
            if (distance<=radius) return ix-1;
        }
        return count;
    }
};

std::vector<uint64_t> orientations(const std::vector<unsigned>& p) {
    unsigned n=p.size(), bit=0;
    std::vector<unsigned> r(n);
    for (unsigned i=0; i<n; ++i) r[p[i]]=i;
    std::vector<uint64_t> b((n*(n-1)/2+63)/64,0);
    for (unsigned i=0; i<n; ++i) for (unsigned j=i+1; j<n; ++j,++bit)
        if (r[i]>r[j]) b[bit/64]|=uint64_t(1)<<(bit%64);
    return b;
}

// A prefix fixes every comparison involving one of its items. All remaining
// comparisons can contribute at most choose(tail,2). This upper bound is
// attained by reversing the reference order on the tail, hence is exact.
template<class Label> unsigned covered_prefix(const std::vector<unsigned>& p,
                                              const Label* ref, unsigned radius) {
    unsigned n=p.size(), fixed=0;
    if (n*(n-1)/2<=radius) return 0;
    for (unsigned i=0; i<n; ++i) {
        for (unsigned j=i+1; j<n; ++j) fixed+=(ref[p[j]]<ref[p[i]]);
        unsigned tail=n-i-1;
        if (fixed+tail*(tail-1)/2<=radius) return i+1;
    }
    throw std::logic_error("Covering permutation did not cover its leaf");
}

// The sum of distances over K centers has an orientation-wise upper bound.
// If that bound is < K*(radius+1), every completion lies in at least one ball.
template<class Label> unsigned collective_prefix(const std::vector<unsigned>& p,
        const Packing<Label>& packing, size_t cover, unsigned best, unsigned radius) {
    if (radius<p.size() || packing.count<2) return best;
    std::vector<size_t> ends={packing.count};
    if (cover+1!=packing.count && cover+1>=2) ends.push_back(cover+1);
    for (auto end:ends) {
        unsigned max_group=std::min(size_t(8),end);
        for (unsigned group=2;group<=max_group;group=std::min(group*2,max_group)) {
            unsigned n=p.size();
            std::vector<uint64_t> loss(n,0), upper(n,0);
            for (unsigned i=0;i<n;++i) for (unsigned j=i+1;j<n;++j) {
                unsigned discord=0;
                for (unsigned k=0;k<group;++k) {
                    auto ref=packing.rank(end-1-k);
                    discord+=(ref[p[i]]>ref[p[j]]);
                }
                loss[i]+=discord;
                upper[i]+=std::max(discord,group-discord);
            }
            uint64_t bound=std::accumulate(upper.begin(),upper.end(),uint64_t(0));
            uint64_t threshold=uint64_t(group)*(radius+1);
            for (unsigned length=0;length<best;++length) {
                if (bound<threshold) {best=length;break;}
                bound-=upper[length]-loss[length];
            }
            if (best==0) return best;
            if (group==max_group) break;
        }
    }
    return best;
}

template<class Label> int run(unsigned n, unsigned radius, double seconds,
                              size_t memory, const std::string& prefix, bool resume, bool joint) {
    auto started=Clock::now();
    auto elapsed=[&](){return std::chrono::duration<double>(Clock::now()-started).count();};
    Packing<Label> packing(n,memory,prefix);
    std::vector<unsigned> p(n); std::iota(p.begin(),p.end(),0);
    uint64_t visited=0, comparisons=0, jumps=0, joint_jumps=0;
    bool more=true;
    if (resume) {
        std::ifstream state(prefix+".state");
        size_t count; unsigned saved_n,saved_radius;
        if (!(state>>saved_n>>saved_radius>>count>>visited>>comparisons>>jumps>>joint_jumps>>more)
            ||saved_n!=n||saved_radius!=radius) throw std::runtime_error("Invalid checkpoint");
        for (auto& x:p) if (!(state>>x)) throw std::runtime_error("Invalid cursor");
        std::ifstream rows(prefix+".orders",std::ios::binary);
        std::vector<unsigned> row(n);
        for (size_t i=0; i<count; ++i) {
            for (auto& x:row) {
                unsigned char lo,hi;
                if (!rows.read(reinterpret_cast<char*>(&lo),1)||!rows.read(reinterpret_cast<char*>(&hi),1))
                    throw std::runtime_error("Truncated checkpoint");
                x=unsigned(lo)+256*unsigned(hi);
            }
            if (!packing.append(row,orientations(row))) throw std::runtime_error("Resume budget too small");
        }
        if (rows.peek()!=EOF) throw std::runtime_error("Unexpected trailing rows");
    }
    std::ofstream output(prefix+".orders",std::ios::binary|(resume?std::ios::app:std::ios::trunc));
    if (!output) throw std::runtime_error("Cannot write candidate checkpoint");
    std::string reason;
    while (more) {
        // Check before each leaf. A leaf scans only the already admitted store.
        if (elapsed()>=seconds) {reason="packing_wall_time_budget";break;}
        if (packing.allocated()>memory) {reason="working_array_memory_budget";break;}
        auto b=orientations(p);
        size_t cover=packing.covering(b,radius,comparisons);
        if (cover==packing.count) {
            if (!packing.append(p,b)) {reason="working_array_memory_budget";break;}
            for (unsigned x:p) {
                output.put(char(x&255)); output.put(char((x>>8)&255));
            }
            if (!output) throw std::runtime_error("Candidate checkpoint write failed");
        }
        ++visited;
        unsigned length=covered_prefix(p,packing.rank(cover),radius);
        if (joint) {
            unsigned shorter=collective_prefix(p,packing,cover,length,radius);
            joint_jumps+=(shorter<length);length=shorter;
        }
        jumps+=(length<n);
        more=advance_prefix(p,length);
    }
    output.close();
    if (!output) throw std::runtime_error("Candidate checkpoint flush failed");
    std::ofstream state(prefix+".state",std::ios::trunc);
    state<<n<<' '<<radius<<' '<<packing.count<<' '<<visited<<' '<<comparisons<<' '<<jumps<<' '<<joint_jumps<<' '<<more<<'\n';
    for (auto x:p) state<<x<<' ';
    state<<'\n'; state.close();
    if (!state) throw std::runtime_error("State write failed");
    struct rusage usage{};
    if (getrusage(RUSAGE_SELF,&usage)!=0) throw std::runtime_error("Cannot read native peak RSS");
#ifdef __APPLE__
    uint64_t rss=usage.ru_maxrss;
#else
    uint64_t rss=uint64_t(usage.ru_maxrss)*1024;
#endif
    std::cout<<std::setprecision(17)<<"{\"complete\":"<<(!more?"true":"false")
        <<",\"reason\":\""<<reason<<"\",\"packing_so_far\":"<<packing.count
        <<",\"visited_leaves\":"<<visited<<",\"distance_comparisons\":"<<comparisons
        <<",\"prefix_jumps\":"<<jumps<<",\"allocated_working_bytes\":"<<packing.allocated()
        <<",\"joint_prefix_jumps\":"<<joint_jumps<<",\"joint_cover\":"<<(joint?"true":"false")
        <<",\"native_peak_rss_bytes\":"<<rss
        <<",\"disk_block_writes\":"<<packing.disk_writes<<",\"disk_block_reads\":"<<packing.disk_reads
        <<",\"elapsed_seconds\":"<<elapsed()<<"}\n";
    return 0;
}

int main(int argc,char** argv) {
    try {
        if (argc!=9) throw std::runtime_error("Expected n radius seconds bytes prefix resume format-version joint-cover");
        unsigned n=std::stoul(argv[1]),radius=std::stoul(argv[2]);
        double seconds=std::stod(argv[3]);size_t memory=std::stoull(argv[4]);
        if (n<2||n>65535||seconds<0||std::string(argv[7])!="1")
            throw std::runtime_error("Unsupported representation or invalid arguments");
        // uint16 is the checkpoint format; the in-memory rank store narrows
        // to uint8 when possible. Neither limit is a statistical item cutoff.
        if (n<=256) return run<uint8_t>(n,radius,seconds,memory,argv[5],std::stoi(argv[6])!=0,std::stoi(argv[8])!=0);
        return run<uint16_t>(n,radius,seconds,memory,argv[5],std::stoi(argv[6])!=0,std::stoi(argv[8])!=0);
    } catch (const std::exception& error) {
        std::cerr<<error.what()<<'\n'; return 2;
    }
}
