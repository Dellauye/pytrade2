#!/bin/bash

public_ip="$(yc compute instance list | grep biml-trade-bots | awk '{print $10}')"
user="yc-user"
tmp_dir="$(pwd)/tmp"
biml_dir="$(pwd)/../.."

prepare_tmp(){
  echo "Cleaning tmp dir: $tmp_dir"
  rm -r -f "$tmp_dir"
  mkdir -p "$tmp_dir/biml"

  echo "Copying biml to tmp"
  cp -r "$biml_dir/biml" "$tmp_dir/biml"

  echo "Preparing biml config"
  rm "$tmp_dir/biml/biml/cfg/app-dev.yaml"
  cp -f "./secret/app.yaml" "./tmp/biml/biml/cfg/"

  echo "Copying docker files"
  for file in  "Dockerfile" "requirements.txt" "docker-compose.yml"
  do
    cp "$biml_dir/$file" "$tmp_dir/biml/"
  done
}

copy_to_remote() {
  echo "Copy biml to $public_ip"
  rsync -v -r "$tmp_dir/biml" $user@"$public_ip":/home/$user/
}

build_docker() {
  echo "Building biml at $public_ip"
  ssh $user@"$public_ip" "cd /home/$user/biml ; sudo docker-compose build lstm"
}

build_baremetal() {
    ssh $user@"$public_ip" "sudo apt install -y pip"
    ssh $user@"$public_ip" "cd /home/$user/biml ; sudo pip install -r requirements.txt"
}

###### Main
prepare_tmp
copy_to_remote
build_docker

#
