from triplea.service.repository import persist

if __name__ == "__main__":
    persist.change_flag_extract_topic(1,0)
    persist.change_flag_affiliation_mining(1,0)
    persist.refresh()

