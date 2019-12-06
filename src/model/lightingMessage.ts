export class LightingMessage{
    private strip: number;
    private brightness: number;
    private pixels: Array<Pixel>;

    constructor(strip: number, brightness: number, pixels: Array<Pixel>){
        this.strip = strip;
        this.brightness = brightness;
        this.pixels = pixels;
    }

    public toUint8(){
        let message = new Uint8Array(1024);
        message[0] = this.strip;
        message[1] = this.brightness;
        let pixelindex = 2;
        this.pixels.forEach((pixel) => {
            message[pixelindex]=pixel.r;
            message[pixelindex+1] = pixel.g;
            message[pixelindex+2] = pixel.b;
            pixelindex += 3;
        });
        return message;
    }
}

export interface Pixel{
    r: number;
    g: number;
    b: number;
}