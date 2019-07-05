# This file start with the planting scheduling model employing the approach #
# that has been used for project scheduling with resource constraints #



class Task():
    """
    This is a task object has information/function about each task
    """
    def __init__(self, number, pre, suc, res, ptime, status):
        self._number = number
        self._pre = pre
        self._suc = suc
        self._res = res
        self._ptime = ptime
        self._ts = None
        self._tf = None
        # status of the task 0 is unscheduled, 1 is scheduled,
        self._status = status

    def schedule_task(self, ts, tf):
        self._tf = tf
        self._ts = ts
        self._status = 1


def update_eligible_activities(tasks):
    """
    This function updates and returns the list of eligible activites
    (and potentially sort it based on some priority rules)
    """
    # initialise the empty D
    D = []
    for free_task in tasks:
        # only deals with the un scheduled tasks
        if free_task._status == 0:
        # if there is no precedence constraint for particular task
            if free_task._pre == None:
                D.append(free_task)
            # elif all of its previous tasks are finished
            elif all(tasks[pre]._status == 1 for pre in free_task._pre):
                D.append(free_task)
    return D

def update_finish_time(F, last_scheduled_task):
    """
    This function updates and returns the finish time of all scheduled tasks
    """
    F.append(last_scheduled_task._tf)
    F.sort()
    return F



def main():
    tasks = [Task(0, None, [1, 2], 0, 0, 0),
            Task(1, [0], [3], 2, 3, 0),
            Task(2, [0], [4], 3, 4, 0),
            Task(3, [1], [5], 2, 2, 0),
            Task(4, [2], [6], 2, 2, 0),
            Task(5, [3], [7], 3, 1, 0),
            Task(6, [4], [7], 2, 4, 0),
            Task(7, [5, 6], None, 0, 0, 0)]

    # S is list of the scheduled tasks
    S = []
    # F is the set of all finish times
    F = []
    # D is the feasible tasks to be scheduled at each stage
    D = []
    # First use dictionary structure for resource dictionary
    Res_D = []

    ts = 0
    tf = ts + tasks[0]._ptime
    tasks[0].schedule_task(ts, tf)

    S.append(tasks[0])
    print('finish', tasks[0]._tf)


    F = update_finish_time(F, tasks[0])
    print('1st F: ', F)
    D = update_eligible_activities(tasks)
    print(D)

    Resouce_total = 4
    Res_D.append((0, Resouce_total))

    for g in range(1, 10):

        print('the resource Availability:', Res_D)
        j = D[0]._number
        print('task to be scheduled = ', j)
        #del D[0]
        # LOOP OVER predecessors of j
        # and get latest finish time, therefore the EF of j is
        # the latest finish time + p(j)
        max_tf = 0
        for i_pre in tasks[j]._pre:
            if tasks[i_pre]._tf > max_tf:
                max_tf = tasks[i_pre]._tf
        print('aaa: ', g, max_tf)
        # get EF of j
        EF = tasks[j]._ptime + max_tf
        print('EF:', EF)
        M = 100
        # loop over the sorted list of predecessors

        res_idx = 0
        while res_idx < len(Res_D) and tasks[j]._status != 1:
            #  loop over the Res_D tuple (time, resouce)
            # if time fits

            print('restime: ', Res_D[res_idx][0])
            print('upper: ',  M - tasks[j]._ptime)
            print('lower: ',  EF - tasks[j]._ptime)

            if Res_D[res_idx][0] <= M - tasks[j]._ptime and \
            Res_D[res_idx][0] >= EF - tasks[j]._ptime:
                print('res index is True for time at index = ', res_idx)

                # and check if the resouce satisfy the task
                print('testing weather the index fits the res constraints')
                for lkidx in range(res_idx, len(Res_D)):
                    print('available res at for this index:',
                    Res_D[lkidx][1])
                    if Res_D[lkidx][1] < tasks[j]._res:
                        print('res at this interval doesnot fit')
                        print('go to the next res interval')
                        res_idx = lkidx + 1
                        break

                    else:
                        # if the resource of lkidx is satisfied
                        # check if the it is the last time point
                        print('avalible:', Res_D[lkidx][1])
                        print('required:', tasks[j]._res)
                        if (res_idx == len(Res_D) -1):
                            print('yes, it is the last element')

                            # if it is the last time points
                            # fit directly
                            tf = Res_D[res_idx][0] + tasks[j]._ptime
                            tasks[j].schedule_task(Res_D[res_idx][0], tf)


                            # the update the Res_D
                            temp_tuple = (Res_D[res_idx][0],
                            Res_D[res_idx][1] - tasks[j]._res)
                            Res_D[res_idx] = temp_tuple

                            Res_D.append((tasks[j]._tf,
                            Resouce_total))



                        elif Res_D[lkidx + 1][0] - Res_D[res_idx][0] \
                        >= tasks[j]._ptime:
                            print('yes, the time length fits')
                            # if time length is enough for the task
                            # schedule the task
                            tf = Res_D[res_idx][0] + tasks[j]._ptime
                            tasks[j].schedule_task(Res_D[res_idx][0], tf)
                            # the new tuple
                            for change_idx in range(res_idx, lkidx + 1):
                                temp_tuple = (Res_D[change_idx][0],
                                Res_D[lkidx][1] - tasks[j]._res)
                                Res_D[change_idx] = temp_tuple
                            # check if the finish time of j is in the list
                            if tasks[j]._tf > Res_D[lkidx + 1][0]:
                                print('and the tf exceeded ')
                                # if finish time is greater than the
                                # interval
                                Res_D.append((tasks[j]._tf,
                                Resouce_total))
                            elif tasks[j]._tf == Res_D[lkidx + 1][0]:
                                # if finish time is on last interval
                                temp_tuple = (Res_D[lkidx + 1][0],
                                Res_D[lkidx + 1][1])
                                Res_D[lkidx + 1] = temp_tuple

                            elif task[j]._tf < Res_D[lkidx + 1][0]:
                                Res_D.insert(lkidx + 1, (tasks[j]._tf,
                                Res_D[lkidx][1] - tasks[j]._res))
                        res_idx = lkidx + 1
                        break
            else:
                res_idx += 1

            
        print('=====================================')
        print('scheduled task number', tasks[j]._number)
        print('scheduled task finish time', tasks[j]._ts)
        print('scheduled task finish time', tasks[j]._tf)
        D = update_eligible_activities(tasks)
        S.append(tasks[j])


        F = update_finish_time(F, tasks[j])

        for i in D:
            print('tasks can be scheduled:', i._number)
        #print('D: ', D)
        #print('S:', S)
        print('F:', F)

        print('===========next g=======================')
        if D == []:
            break
    print('Final resource overview:', Res_D)
    for i in S:
        print('task schedule sequence:', i._number)
main()

# class ScheduledTask():
#     """
#     This is a scheduled task which has the
#     """
#     def __init__(self, task, ts):
#         self.task = task
#         self.ts = ts




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
