from run import Publication, db

oxford = Publication(100, 'Oxford Publication')
paramount = Publication(102, 'Paramount Press')
oracle = Publication(103, 'Oracle Inc.')

db.session.add_all([oxford, paramount, oracle])
db.session.commit()
