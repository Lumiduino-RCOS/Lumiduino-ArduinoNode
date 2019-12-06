import * as serialport from 'serialport';
import SerialPort = require('serialport');
import {LightingMessage, Pixel} from './model/lightingMessage';
//import * as SerialPort from 'serialport';

export class Arduino{
    private serialConnection: SerialPort;
    private parser: SerialPort.parsers.Readline;

    constructor(arduinoAddress: string, baud: number){
        this.serialConnection = new SerialPort(arduinoAddress, {
            baudRate: baud,
        });
        this.parser = new SerialPort.parsers.Readline({
            delimiter: "\n"
        });
        this.serialConnection.pipe(this.parser);
        this.parser.on('data', (message) => this.onMessage(message));
        this.serialConnection.on('error', (err) => this.onError(err));
        this.serialConnection.on('close', () => this.onClose());
        this.sendTester();
    }

    private onMessage(message: string){
        console.log(message);
    }

    private onError(error){
        console.error(error);
    }

    private onClose(){
        console.log("The serial connection has closed");
    }

    private sendTester(){
        setInterval(() => {
            //this.serialConnection.write("ASDASD\n");
            let pixelArray = new Array<Pixel>();
            let pix: Pixel = {
                r: 255,
                g: 100,
                b: 10
            };
            for(let i=0; i< 100; i++){
                pixelArray.push(pix);
            }
            let message = new LightingMessage(0, 255, pixelArray);
            /*let x = Buffer.alloc(1024);
            for(let i =0;i<5; i++){
                x[i*3+1] = 25;
                x[i*3+2] = 20;
                x[i*3+3] = 100;
            }*/
            this.serialConnection.write(message.toUint8()+'\n');
            console.log(message.toUint8());
            //this.parser.write("");
        }, 1000);
    }
}
