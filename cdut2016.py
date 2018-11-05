import datetime

from app import create_app, db, scheduler
from app.models import User
from app.news_cdut.models import NewsCdut

app = create_app()
app.app_context().push()
# 启动后台任务
scheduler.add_job(func='app.task:init', args='', next_run_time=datetime.datetime.now(), id='init')
scheduler.add_job(func='app.task:update_cdut', args='', trigger='interval', seconds=6000, id='update')
scheduler.add_job(func='app.task:update_score', args='', trigger='interval', seconds=60, id='update_2')
scheduler.start()
app.run()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'newscdut': NewsCdut}
