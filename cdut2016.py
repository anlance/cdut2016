import datetime

from app import create_app, db, scheduler
from app.models import User
from app.news_cdut.models import NewsCdut

app = create_app()
app.app_context().push()
# 启动后台任务
scheduler.add_job(func='app.task:update_cdut', args='',trigger='interval', seconds=10, id='update')
# scheduler.add_job(func='app.task:save', args='', trigger='interval', seconds=1800, id='cron_task')
scheduler.start()
app.run()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'newscdut': NewsCdut}
