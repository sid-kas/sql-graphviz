
get_all_table_names = """
    SELECT 
        name
    FROM 
        sqlite_master 
    WHERE 
        type ='table' AND 
        name NOT LIKE 'sqlite_%';
"""
get_table_pragma = """
    PRAGMA table_info (?)
"""
