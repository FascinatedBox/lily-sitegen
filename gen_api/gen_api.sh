mkdir -p api_dir
mkdir -p output/embed
mkdir -p nat_dir
cp ~/Desktop/ecosystem/lily/src/lily.h api_dir/lily.h
naturaldocs -i api_dir -o html output/api -p nat_dir > /dev/null
