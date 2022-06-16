import geopandas
import pandas
import numpy
"""
code for calculating steepness level and the minimum qualifying sl for each link with regard to directionality 
"""

def calc_SL(length, slope):  # calculates SL for different SL aspirations (segments shorter than 50 always qualify)
    if length> 51:
        slope = abs(slope)
        sl_35, sl_5 = 99, 99
        if slope <= 0.035:
            sl_35, sl_5 = 3.5, 5
        elif slope <= 0.05:
            sl_5 = 5
            if length <= 500:
                sl_35 = 3.5
        elif slope <= 0.065:
            if length <= 150:
                sl_35, sl_5 = 3.5, 5
            elif length <= 500:
                sl_5 = 5
        elif slope <= 0.08:
            if length <= 150:
                sl_5 = 5
        # elif slope < 0.095:
        #     if length < 500:
        #         SL500 = 8
        #     if length < 150:
        #         SL150 = 6.5
    else:
        sl_35, sl_5 = 3.5, 5
    return sl_35, sl_5

def sl_signage(slope, sl):
    return sl if slope>0 else sl*(-1)

# if __name__ == '__main__':
#     streets = geopandas.read_file(
#
#         'C:\\Users\\bitas\\folders\\Research\\Montreal\\codes\\accessibility\\data\\downtown_test.gpkg')
#
#
#     streets[['lts', 'lts_c', 'length', 'slope_edit']] = streets[['lts', 'lts_c', 'length', 'slope_edit']].replace(numpy.nan, 0)

#     #calculate steepness level and set the minimum valid SL for each line
#     streets[['sl_35', 'sl_5']] = streets.apply(lambda row: pandas.Series(calc_SL(row['length'], row['slope_edit'])),
#                                        axis=1)
#     streets['unsigned_sl'] = streets.apply(lambda row: min(row['sl_35'], row['sl_5']), axis=1)
#
#     # if slope is positive signed_SL would be + else -
#     streets['signed_sl'] = streets.apply(lambda row: sl_signage(row['slope_edit'], row['unsigned_sl']), axis =1)