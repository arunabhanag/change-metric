#!/bin/sh           

sourcedir="../E99-Language-Learning"
hasher="php func-hash.php -p $sourcedir/backend;$sourcedir/apis"
gitbranch="back-end-working"

datadir="data"
commits="$datadir/commits.txt"

git_cmd="git --git-dir $sourcedir/.git --work-tree $sourcedir"




rm $datadir/*

#get all the commit hashes
$git_cmd log -20 --pretty=format:"%h - %ad" > $commits

#go through each commit, hash the functions
for commit in `cat $commits | cut -d ' ' -f1`
do 
    $git_cmd checkout $commit
	$hasher > "$datadir/hash_$commit.txt"
done

#go back to the HEAD
$git_cmd checkout $gitbranch

