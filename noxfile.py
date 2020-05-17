import nox

@nox.session
def tests(session):
    session.install('pytest')
    session.install('.')
    session.run('pytest')

