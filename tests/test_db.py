
from triplea.db.tinydb import DB_TinyDB
from triplea.service.click_logger import logger

if __name__ == '__main__':
    db = DB_TinyDB()
    data = db.get_article_group_by_state()
    for i in range(-3,7):
        w = 0
        for s in data:
            if s['State'] == i:
                w = 1
                n = s['n']
                logger.INFO(f'{n} article(s) in state {i}.')
        if w == 0 : 
            logger.INFO(f'0 article(s) in state {i}.')
            
            

    