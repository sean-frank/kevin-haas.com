import os
from dotenv import load_dotenv


def get_app_root(rel_path):
	app_root = os.path.abspath(rel_path)

	if os.path.isfile(rel_path):
		app_root = os.path.dirname(os.path.abspath(rel_path))

	return app_root

def get_configs(app_root):
	dotenv_path = os.path.join(app_root, '.env')
	load_dotenv(dotenv_path=dotenv_path)
	return os.getenv

