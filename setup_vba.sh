# Be sure this script is within the top-level of the vb-archiver project folder
echo "Installing prerequisite files..."
pip install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl
mkdir dldest
npm install