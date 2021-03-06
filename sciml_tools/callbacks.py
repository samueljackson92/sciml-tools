import time
import mlflow
import tensorflow as tf
import numpy as np
from sciml_tools.system import DeviceLogger

class EnergyCallback(tf.keras.callbacks.Callback):

    def __init__(self):
        self._logger = DeviceLogger(interval=0.5)

    def on_train_begin(self, logs=None):
        self._start_time = time.time()
        self._logger.start()

    def on_train_end(self, logs=None):
        self._logger.stop()
        self._end_time = time.time()
        self._duration = self._end_time -  self._start_time

    @property
    def metrics(self):
        power_metrics = self._logger.metrics

        total_milliwatts = 0
        for key, value in power_metrics.items():
            total_milliwatts += np.mean(power_metrics[key])

        # Conversion factors for Green house gasses for UK grid.
        # https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2019
        conversion_factors = dict(
                co2e=0.2556,
                co2=0.25358,
                ch4=0.00065,
                n2o=0.00137)

        total_kilowatts = total_milliwatts * 1e-6
        total_hours = self._duration / 3600
        kilowatt_hours = total_hours * total_kilowatts

        metrics = {}
        for name, factor in conversion_factors.items():
            metrics[name] = factor * kilowatt_hours

        metrics['total_kilowatt_hours'] = kilowatt_hours
        return metrics

class MLFlowEnergyCallback(EnergyCallback):

    def __init__(self):
        super(MLFlowEnergyCallback, self).__init__()

    def on_train_end(self, logs=None):
        super().on_train_end()
        mlflow.log_metrics(self.metrics)
