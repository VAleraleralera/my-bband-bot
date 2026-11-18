# --- Не удаляйте эти библиотеки ---
from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


# --------------------------------


class BbandRsi(IStrategy):
 """

 автор@: Герт Вольгемут

 переведено с:

 https://github.com/sthewissen/Mynt/blob/master/src/Mynt.Core/Strategies/BbandRsi.cs

 """

 INTERFACE_VERSION: int = 3
 # Минимальная рентабельность инвестиций, рассчитанная для стратегии.
 # корректируется в зависимости от рыночных условий. Мы рекомендуем устанавливать низкий показатель для быстрого возврата инвестиций.
 # Этот атрибут будет переопределен, если в файле конфигурации указан параметр "minimal_roi"
 minimal_roi = {
 "0": 0.1
 }

 # Оптимальный стоп-лосс для стратегии
 stoploss = -0.25

 # Оптимальный таймфрейм для стратегии
 timeframe = '1h'

 def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
 dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

 # Полосы Боллинджера
 bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
 dataframe['bb_lowerband'] = bollinger['lower']
 dataframe['bb_middleband'] = bollinger['mid']
 dataframe['bb_upperband'] = bollinger['upper']

 return dataframe

 def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
 dataframe.loc[
 (
 (dataframe['rsi'] < 30) &
 (dataframe['close'] < dataframe['bb_lowerband'])

 ),
 'enter_long'] = 1
 return dataframe

 def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
 dataframe.loc[
 (
 (dataframe['rsi'] > 70)

 ),
 'exit_long'] = 1
 return dataframe
