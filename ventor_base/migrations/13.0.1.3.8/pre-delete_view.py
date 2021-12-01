def migrate(cr, version):
    if not version:
        return

    cr.execute("""
        DELETE FROM ir_ui_view WHERE name='Users Preferences';
    """)
