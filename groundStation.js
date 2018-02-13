//ポート
const PORTNUM = 7;

const serialPort = require('serialport');

//シリアルポート設定
const sp = new serialPort('COM' + PORTNUM, {
	baudRate: 9600,
	dataBits: 8,
	parity: 'none',
	stopBits: 1,
});

const ready = serialPort.parsers.Ready;
const fs = require('fs');
const spawnSync = require('child_process').spawnSync;

//COMオープン
sp.open(function(){
	console.log('Open COM' + PORTNUM);
});

//エラー時メッセージ表示
sp.on('error', function(err){
	console.log('<ERROR>: ', err);
});

//データ受信（デリミタ受信 → downlink_confirm実行）
connection_confirm();

function connection_confirm(){
	const parserReady = sp.pipe(new ready({ delimiter: '#' }));
	parserReady.on('ready', downlink_confirm);

	function downlink_confirm() {
		console.log('Receive DELIMITER');
		console.log('Start: downlink_confirm');

		sp.on('readable', function(){
			var downlink_confirm_text = sp.read(5);
			console.log(downlink_confirm_text);
		});

		if(downlink_confirm_text == "Hello")
		  console.log("Success");
		else {
			console.log("Failed");
		}

	}
}
