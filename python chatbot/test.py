def test_project_runs():
    try:
        import main
    except Exception as e:
        assert False, f"Error: {e}"
