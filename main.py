import itertools, os, shutil

start_dir = ''
trash_dir = ''
dry_run = False

all_files = dict()

for dir_path, dirs, files in os.walk(start_dir):
    for f_name in files:
        f_path = os.path.join(dir_path, f_name)
        f_size = os.path.getsize(f_path)
        rel_path = os.path.relpath(dir_path, start_dir)
        all_files.setdefault((f_name, f_size), []).append(rel_path)

duplicated_files_count = 0
duplicates_count = 0
space_to_free_up = 0
duplicates = dict()
for file, dirs in all_files.items():
    count = len(dirs)
    if count > 1:
        duplicated_files_count += 1
        duplicates_count += count
        space_to_free_up += (count - 1) * file[1]
        for d1, d2 in itertools.combinations(dirs, 2):
            duplicates.setdefault((d1, d2), []).append(file)

sorted_duplicates = sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)
print(f'Total unique files: {len(all_files)}')
print(f'Duplicated files: {duplicated_files_count}')
print(f'Total duplicates: {duplicates_count}')
print(f'Cases to resolve: {len(sorted_duplicates)}')
print(f'Disk space to free up: {space_to_free_up / (1024 * 1024) :.1f}Mb1 ')


for dirs, files in sorted_duplicates:
    print('================================')
    print(f'{len(files)} duplicates in {dirs[0]} and {dirs[1]}')
    for f in files:
        also_present = [d for d in all_files[f] if d not in dirs]
        print(f[0], f'(also present in {", ".join(also_present)})' if also_present else '')

    command = input(f'1: keep {len(files)} files in {dirs[0]}\n2: keep {len(files)} files in {dirs[1]}\nEnter: skip\n')

    def move_files_from(src_dir):
        src_dir = src_dir.strip('.')
        dst_path = os.path.join(trash_dir, src_dir)
        os.makedirs(dst_path, exist_ok=True)
        for f in files:
            src_path = os.path.join(start_dir, src_dir, f[0])
            if dry_run:
                print(f'Move {src_path} to {dst_path}')
            else:
                shutil.move(src_path, os.path.join(dst_path, f[0]))

    if command == '1':
        move_files_from(dirs[1])
    elif command == '2':
        move_files_from(dirs[0])
