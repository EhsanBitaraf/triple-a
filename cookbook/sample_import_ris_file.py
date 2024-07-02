from triplea.service.repository.import_file.ris_parser import import_ris_file
import triplea.service.repository.persist as PERSIST

if __name__ == "__main__":
    
    # Improt RIS format from Web Of Sicience
    import_ris_file("wos.ris")
    PERSIST.refresh()

