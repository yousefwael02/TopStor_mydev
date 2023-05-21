#/bin/sh

cd /
mkdir top2
cd top2
git init
git checkout -b QSD3.07
git remote add localgit http://10.11.11.252/git/TopStordev.git
git remote add remotegit https://github.com/MoatazNegm/TopStordev.git
git pull remotegit QSD3.07
echo '###################################################'
git show | grep commit
echo '###################################################'

cd /
mkdir pac2
cd pac2 
git init
git checkout -b QSD3.07
git remote add localgit http://10.11.11.252/git/HC.git
git remote add remotegit https://github.com/MoatazNegm/HC.git
git pull remotegit QSD3.07
echo '###################################################'
git show | grep commit
echo '###################################################'

cd /
mkdir web2 
cd web2
git init
git checkout -b QSD3.07
git remote add localgit http://10.11.11.252/git/TopStorweb.git
git remote add remotegit https://github.com/MoatazNegm/TopStorWeb.git
git pull remotegit QSD3.07
echo '###################################################'
git show | grep commit
echo '###################################################'



