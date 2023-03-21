# Be sure this script is within the top-level of the vb-archiver project folder
echo "Installing prerequisite files..."
mkdir .venv
python -m venv ./.venv/
mkdir .vscode
echo "{\"python.defaultInterpreterPath\":\"\${workspaceFolder}/.venv/Scripts/python.exe\",\"python.pipenvPath\":\"\${workspaceFolder}/.venv/Scripts/pip.exe\"}" > ./.vscode/settings.json
pip install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl
pip install dicttoxml
mkdir dldest
mkdir -p ./gui/node_modules/
npm install --prefix ./gui/node_modules/