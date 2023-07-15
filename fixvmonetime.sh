#/bin/sh
branch=$1
cd /
rm -rf top2
mkdir top2
cd top2
git init
git checkout -b QSD3.07
git remote add origin http://10.11.11.252/git/TopStordev.git
git pull origin QSD3.07
echo '###################################################'
git show | grep commit
echo '###################################################'

cd /
rm -rf pac2
mkdir pac2
cd pac2 
git init
git checkout -b $branch 
git remote add origin http://10.11.11.252/git/HC.git
git pull origin $branch 
echo '###################################################'
git show | grep commit
echo '###################################################'

cd /
rm -rf web2
mkdir web2 
cd web2
git init
git checkout -b $branch 
git remote add origin http://10.11.11.252/git/TopStorweb.git
git pull origin $branch 
echo '###################################################'
git show | grep commit
echo '###################################################'
echo moving new directories
cd /
rm -rf /TopStor /pace /topstorweb
mv /top2 /TopStor
mv /pac2 /pace
mv /web2 /topstorweb
rm -rf top2
rm -rf pac2
rm -rf web2
cd /TopStor
./systempull.sh $branch 
cd /
cd /TopStor
git show | grep commit
sync
sync
echo finished
