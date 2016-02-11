import os

root_folder = '/Users/Jogi/Development/Projects/Photography-J'
album_folder = 'albums/san_francisco'

full_path = os.path.join(root_folder, album_folder)

for a_file in os.listdir(full_path):
	if not a_file.startswith('.DS_Store') and not a_file.startswith('album_thumb'):
		print "  - path: '/%s'" % os.path.join(album_folder, a_file)

