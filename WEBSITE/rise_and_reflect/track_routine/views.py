from datetime import date
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import RoutineTasks
from tasks.models import PersonalTasks, Tasks, TrackedTasks
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


# TODO:
# Separate evening from morning
# create new view to handle changing days on page

def track_routine(request):

    # get user
    user = request.user
    # Get user tasks
    # get duration and task_id of the users tasks
    all_user_tasks_tuple = PersonalTasks.objects.filter(user=request.user).values_list(
        "id", "duration", "task_id"
    )
    # turn it to a list of lists
    all_user_tasks_list = [list(j) for j in all_user_tasks_tuple]

    if request.POST:
        # list of tasks that are ticked
        tasks = [int(item) for item in list((request.POST).dict().values()) if item.isdigit()]
        # List of all tasks of user
        all_user_tasks_ids = [item[2] for item in all_user_tasks_list ]

        # Run through all the users personal tasks
        for count, task in enumerate(all_user_tasks_ids):
            # check to see is that task is ticked
            if task in tasks:
                # set that task to true
                TrackedTasks.objects.filter(personal_task=PersonalTasks.objects.get(task_id=Tasks.objects.get(id=task), user=user)).update(completed=True)
            else:
                # Set that task to false
                TrackedTasks.objects.filter(personal_task=PersonalTasks.objects.get(task_id=Tasks.objects.get(id=all_user_tasks_ids[count]), user=user)).update(completed=False)

    # for every task of the users
    for task in range(len(all_user_tasks_list)):
        # Get the task with the id
        filtered_task = Tasks.objects.get(id=all_user_tasks_list[task][2])
        # Then add type and task to list
        all_user_tasks_list[task].append(filtered_task.task_type)
        all_user_tasks_list[task].append(filtered_task.task_type)
        all_user_tasks_list[task].append(filtered_task.task)
        all_user_tasks_list[task].append(filtered_task.custom)
    # filter RoutineTasks for user to check if a routine exists
    routine = RoutineTasks.objects.filter(user=user)

    # If a routine exists
    if routine:
        routine_check = RoutineTasks.objects.filter(day=timezone.now(), user=user).first()
        try:
            # check if routine exists for today
            routine_check = RoutineTasks.objects.filter(day=timezone.now(), user=user, routine_type="Morning").first()
        # If it is a custom one
        except:
            routine_check = RoutineTasks(user=user, routine_type="Morning")
            routine_check.save()

        # get duration and task_id of the users tasks
        all_user_tasks_tuple = PersonalTasks.objects.filter(
            user=request.user
        ).values_list("duration", "task_id")
        # turn it to a list of lists
        all_user_tasks_list = [list(j) for j in all_user_tasks_tuple]
        

        # for every task of the users
        for task in range(len(all_user_tasks_list)):
            # Get the task using the id
            filtered_task = Tasks.objects.get(id=all_user_tasks_list[task][1])
            # Then add type and task to list
            all_user_tasks_list[task].append(filtered_task.task_type)
            all_user_tasks_list[task].append(filtered_task.task)
            all_user_tasks_list[task].append(filtered_task.custom)

            filter_by_this_task = PersonalTasks.objects.get(task_id = filtered_task, user=request.user)
            tracked_task = TrackedTasks.objects.get(personal_task = filter_by_this_task,  personal_routine=routine_check)
            
            all_user_tasks_list[task].append(tracked_task.completed)

        if routine_check:
            return render(
                request, "routine/track_routine.html", {"routine": all_user_tasks_list}
            )

    return render(
        request, "routine/track_routine.html", {"add_tasks": "you need to create tasks and/or go to Create Routine."}
    )

# TODO: Get drag and drop and position working
class RoutineSortingView(View):
    # def post(self, request, pk, *args, **kwargs):
    #     for index, pk in enumerate(request.POST.getlist('book[]')):
    #         book = get_object_or_404(Book, pk=pk)
    #         book.position = index
    #         book.save()
    #     return HttpResponse()

    @csrf_exempt
    def sort(self):
        tasks_ordered = json.loads(self.request.POST.get("sort"))
        for t in tasks_ordered:
            ordered_task = get_object_or_404(RoutineTasks, pk=int(t["pk"]))
            ordered_task.position = t["order"]
            ordered_task.save()
        return HttpResponse("saved")
