# Be sure this script is within the top-level of the vb-archiver project folder
echo "Making Directories ... " && \
mkdir .venv && \
python -m venv ./.venv/ && \
mkdir .vscode && \
mkdir dldest && \
mkdir -p ./gui/node_modules/ && \
echo "{\"python.defaultInterpreterPath\":\"\${workspaceFolder}/.venv/Scripts/python.exe\",\"python.pipenvPath\":\"\${workspaceFolder}/.venv/Scripts/pip.exe\"}" > ./.vscode/settings.json && \
exec $SHELL && source setup_vba.sh
echo "Installing prerequisite files ... "
pip install git+https://github.com/ytdl-org/youtube-dl.git@master#egg=youtube_dl
pip install dicttoxml
npm install --prefix ./gui/node_modules/