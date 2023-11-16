from celery import shared_task

@shared_task
def prueba_task():
    print("¡La tarea de prueba está funcionando!")