# Be sure this script is within the top-level of the vb-archiver project folder
echo "Making Directories ... "
mkdir .venv
python -m venv ./.venv/
mkdir .vscode
mkdir dldest
mkdir -p ./gui/node_modules/
echo "{\"python.defaultInterpreterPath\":\"\${workspaceFolder}/.venv/Scripts/python.exe\",\"python.pipenvPath\":\"\${workspaceFolder}/.venv/Scripts/pip.exe\"}" > ./.vscode/settings.json
echo "Activating virtual env ... "
source ./.venv/Scripts/activate
echo "Installing prerequisite files ... "
pip install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl
pip install dicttoxml
pip install schema
npm install
