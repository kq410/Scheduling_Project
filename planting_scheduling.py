# This file start with the planting scheduling model employing the approach #
# that has been used for project scheduling with resource constraints #



class Task():
    """
    This is a task object has information/function about each task
    """
    def __init__(self, pre, suc, res, ptime):
        self._pre = pre
        self._suc = suc
        self._res = res
        self._ptime = ptime
        self.ts = None



def main():
    task_zero = Task(None, [task_one, task_two], 0, 0)
    task_one = Task([task_zero], [task_three], 2, 3)
    task_two = Task([task_zero], [task_three], 3, 4)
    task_three = Task([task_one], [task_five], 4, 2)
    task_four = Task([task_two], [task_six], 4, 2)
    task_five = Task([task_three], [task_seven], 3, 1)
    task_six = Task([task_four], [task_seven], 2, 4)
    task_seven = Task([task_five, task_six], None, 0, 0)

class ScheduledTask():
    """
    This is a scheduled task which has the
    """
    def __init__(self, task, ts):
        self.task = task
        self.ts = ts




class PlantingSchedule():
    """

    """

class PlanterAvailability():
    """
    90% of the work
    """

class ScheduleManager():
    """
    This would be the manager of the schedule
    """
