# Be sure this script is within the top-level of the vb-archiver project folder
echo "Installing prerequisite files..."
mkdir venv
python -m venv ./venv/
pip install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl
mkdir dldest
mkdir -p ./gui/node_modules/
npm install --prefix ./gui/node_modules/