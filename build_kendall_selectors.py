"""Join saved discovery choices to the chosen predictor's distance; never reselect."""
import math
import numpy as np
import pandas as pd
import build_heldout_kendall as a


def chosen(base,lookup,choice,primary,expected,selector):
    template=lookup[primary]
    row=dict(template)
    if choice=='abstain':
        row.update(status='abstain',nll=math.nan,test_kendall_mean=math.nan,test_kendall_sum=math.nan)
    else:
        row=dict(lookup[primary if choice=='sm' else 'pl'])
    np.testing.assert_allclose(row['nll'],expected,atol=2e-8,rtol=2e-8,equal_nan=True)
    row.update(base,method=selector,selected_method=choice,alias_of=primary if choice=='sm' else choice)
    a.ROWS.append(row)


def main():
    for part in ('bridge','shell','coverage'):
        fits=a.frame(f'results/heldout_kendall/strict_{part}_fits.csv.gz')
        index={(int(c),int(rep)):g.set_index('method').to_dict('index') for (c,rep),g in fits.groupby(['cell','repeat'])}
        for row in a.frame(f'results/strict_features/{part}_selection_replicates.csv').to_dict('records'):
            for selector in ('pair','context'):
                chosen(dict(study='D1',setting=f"{part}-cell{row['cell']}",source=f'results/strict_features/{part}_selection_replicates.csv'),
                       index[row['cell'],row['rep']],row[selector+'_choice'],row['primary_sm'],row[selector+'_selected_nll'],selector)
        if part=='bridge':
            for row in a.frame('results/strict_features/followup_budget_replicates.csv').to_dict('records'):
                chosen(dict(study='D1_budget',setting=f"cell{row['cell']}-budget{row['budget']}",source='results/strict_features/followup_budget_replicates.csv'),
                       index[row['cell'],row['rep']],row['choice'],'mle',row['selected_nll'],row['selector'])
    fits=a.frame('results/heldout_kendall/repeated_fits.csv.gz');fits=fits[fits.split=='confirmation']
    index={(ds,int(rep)):g.set_index('method').to_dict('index') for (ds,rep),g in fits.groupby(['dataset','repeat'])}
    for row in a.frame('results/repeated_holdout/repeat_selections.csv.gz').to_dict('records'):
        chosen(dict(study='P1_selection',source='results/repeated_holdout/repeat_selections.csv.gz'),
               index[row['dataset'],row['repeat']],row['choice'],'mle',row['confirmation_nll'],row['selector'])
    fits=a.frame('results/heldout_kendall/fixed_real_fits.csv.gz');fits=fits[fits.split=='confirmation']
    index={ds:g.set_index('method').to_dict('index') for ds,g in fits.groupby('dataset')}
    for row in a.frame('results/strict_features/real_selection.csv').to_dict('records'):
        for selector in ('pair','context'):
            chosen(dict(study='P2_selection',source='results/strict_features/real_selection.csv'),
                   index[row['dataset']],row[selector+'_choice'],'mle',row[selector+'_confirmation_nll'],selector)
    a.output('selectors')


if __name__=='__main__':main()
