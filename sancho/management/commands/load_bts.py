# python imports
from pathlib import Path
import pandas as pd

# django imports
from django.core.management.base import BaseCommand
from django.conf import settings

# project imports
from sancho.models import Backtest, Metrics


class Command(BaseCommand):
    help = 'Adds data from an Excel file to the database'

    # This function add the arguments to the command.
    # It expects an excel file, which will be stored in options['bts_file']
    def add_arguments(self, parser):
        parser.add_argument("bts_file", nargs='+', type=str)
    

    def handle(self, *args, **options):        
        print(f'Starting the data import...')
        print(f'##########################################################################################')
        if options['bts_file'][0].endswith('xlsx'):
            bts = pd.read_excel(options['bts_file'][0], index_col=0, engine='openpyxl')
                
        if len(bts.index) > 0:
            '''
            engine = create_engine('sqlite:///db.sqlite3')
            bts.to_sql(Backtest._meta.db_table, if_exists='append', on=engine, index=True) 
            bts.to_sql(Metrics._meta.db_table, if_exists='append', con=engine, index=True)
            '''
            for ix in bts.index:
                name = 'BT' + str(bts.index[ix])
                symbol = bts.loc[ix]['Symbol']
                timeframe = bts.loc[ix]['TF']
                ordertype = bts.loc[ix]['OrderType']
                # Convert to database format
                if (ordertype=='Buy'):
                    ordertype = Backtest.OrderType.BUY
                elif (ordertype=='Sell'):
                    ordertype = Backtest.OrderType.SELL
                
                # Create object for backtest 
                bt = Backtest(name=name,
                              symbol=symbol,
                              ordertype=ordertype,
                              timeframe=timeframe)
                
                profit = bts.loc[ix]['BN']
                num_ops = bts.loc[ix]['NumOps']
                pf = bts.loc[ix]['PF']
                rf = bts.loc[ix]['RF']
                dd = bts.loc[ix]['DD']
                ep = bts.loc[ix]['EP']
                pct_winner = bts.loc[ix]['Pct_win']
                kratio = bts.loc[ix]['kratio']
                best_operation_pips = bts.loc[ix]['BestOp']
                worst_operation_pips = bts.loc[ix]['WorstOp']
                max_losing_strike = bts.loc[ix]['Max_Loss_Strike']
                max_winning_strike = bts.loc[ix]['Max_Win_Strike']
                max_exposure = bts.loc[ix]['Max_Exposure']
                sqn = bts.loc[ix]['SQN']
                avg_win = bts.loc[ix]['Avg_Win']
                avg_loss = bts.loc[ix]['Avg_Loss']
                closing_days = bts.loc[ix]['Days']

                # Create object for metrics
                mt = Metrics(backtest = bt,
                             profit=profit,                             
                             num_ops=num_ops,
                             pf=pf,
                             rf=rf,
                             dd=dd,
                             ep=ep,
                             kratio=kratio,
                             pct_winner=pct_winner,
                             max_losing_strike=max_losing_strike,
                             max_winning_strike=max_winning_strike,
                             max_exposure=max_exposure,
                             best_operation_pips=best_operation_pips,
                             worst_operation_pips=worst_operation_pips,
                             sqn=sqn,
                             avg_win=avg_win,
                             avg_loss=avg_loss,
                             closing_days=closing_days,
                             loss=0,
                             max_lots=0,
                             min_lots=0,
                             sharpe_ratio=0)
                
                print(f'Adding to database backtest {ix} of {len(bts.index)}')
                # Commit both objects to database
                bt.save()
                mt.save()

        print(f'##########################################################################################')
