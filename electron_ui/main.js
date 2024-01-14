const { app, BrowserWindow, ipcMain } = require('electron');
const { exec } = require('child_process');
let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    });
    mainWindow.loadFile('templates/index.html');
    mainWindow.setMenu(null);
}

app.whenReady().then(() => {
    createWindow();
    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

ipcMain.on('page-not-found', (event, pagePath)=>{
    if(pagePath === '/'){
        mainWindow.loadFile('./templates/index.html');
    }else{
        mainWindow.loadFile('./templates/undefined.html');
    }
})

app.on('window-all-closed', function () {
    if (process.platform!== 'darwin') {
        app.quit();
    }
});