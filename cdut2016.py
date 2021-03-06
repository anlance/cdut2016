import datetime

from app import create_app, db, scheduler
from app.models import User
from app.news_cdut.models import NewsCdut

app = create_app()
app.app_context().push()
# 启动后台任务
scheduler.add_job(func='app.task:init', args='', next_run_time=datetime.datetime.now(), id='init')
scheduler.add_job(func='app.task:update_score', args='', trigger='interval', seconds=600, id='update_2')
scheduler.add_job(func='app.task:init_cdut', args='', trigger='interval', seconds=36000, id='cdut_news')
scheduler.start()
app.run()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'newscdut': NewsCdut}
