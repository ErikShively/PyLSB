#!/usr/bin/python3
from skimage import io
import numpy as np
import filetype
import argparse

class frame:
    #Constructor
    def __init__(self) -> None:
        self.dataToEncode = []
        self.maxEncode = None
        self.hostImage = None
        self.encLen = None
        self.maxEncode = None
        self.pixCont = None

    def _int2bList(self, intInput, bitCont=8) -> list:

        """
        Converts an integer to a list of the bits used to represent the number

        Parameters:
        intInput: An int to get converted
        bitCont: An int to specify how to pad the list

        Returns:
        List: The list containing bits to represent the iteger input
        """

        return list(map(int,list(bin(intInput)[2:].zfill(bitCont))))

    def openFile(self, fileHandle, parseText=False, encoding="utf-8") -> bool:

        """
        Opens a file to encode into the host image

        Parameters:
        fileHandle: The path of the file to open
        parseText: Bool to determine whether to process the file as text
        encoding: The encoding of the text, provided praseText is True
        
        Returns:
        Success: A bool indicating if the operation was performed successfully
        """

        if(parseText==True):
            with open(fileHandle, "r") as f:
                for line in f:
                    for byte in line.encode(encoding):
                        self.dataToEncode += self._int2bList(byte, 8)
        else:
            Bytes = np.fromfile(fileHandle, dtype="uint8")
            self.dataToEncode = list(np.unpackbits(Bytes))
        return True

    def openHost(self, imgHandle) -> None:

        """
        Opens a host image

        Parameters:
        imgHandle: Path of file to open
        """

        self.hostImage = io.imread(imgHandle)
        self.pixCont = (self.hostImage.shape[0] * self.hostImage.shape[1])
        self.encLen = self.pixCont.bit_length()
        self.maxEncode = self.pixCont - self.encLen

    def encodeImg(self, handle="output.png") -> bool:
        """
        Encodes data to host. Takes the output image handle. Returns True if successful.

        Parameters:
        Handle: File path for data

        Returns:
        Successful: Bool indicating if operation was successful
        """
        imgX = -1
        bitList = self._int2bList(len(self.dataToEncode), self.encLen) + self.dataToEncode
        
        if((filetype.guess(handle).extension == "jpg") | (filetype.guess(handle).extension == "jpeg")):
            print("Detecting a lossy format. Forcing host to png.")
            handle += ".png"

        if(len(bitList) <= self.pixCont):
            for index,bit in enumerate(bitList):
                imgY = index%len(self.hostImage[0])
                if(imgY==0):
                    imgX += 1
                encPix = list(bin(self.hostImage[imgX][imgY][0]))
                encPix[-1] = str(bit)
                self.hostImage[imgX][imgY][0] = (int("".join(encPix),2))
            io.imsave(handle, self.hostImage)
            return True
        else:
            print("Data to encode is larger than image size. Aborting.")
            return False
            
    def decodeImg(self, outFile="output", verbose=False) -> bool:
        """
        Decodes image. Takes output handle, verbosity (see arguments). Returns true if successful.

        Parameters:
        OutFile: The handle of the output file
        Verbose: Bool to determine whether or not the output should be printed

        Returns:
        Successful: Bool indicating if operation was successful
        """
        lenBin = '0b'
        finished = False
        index = 0
        imgX = -1
        imgY = 0
        dataToDecode = []
        while(finished == False):
            imgY = index%len(self.hostImage[0])
            if(imgY == 0):
                imgX += 1

            if(len(lenBin) > self.encLen+1):
                dataLen = int(lenBin,2)
                if(dataLen > self.pixCont):
                    print("Encoded key implies data that cannot be stored in this image. \n It's probably not encoded")
                    return False
                else:
                    finished = (index >= (dataLen+self.encLen-1))
                    dataToDecode.append(int(bin(self.hostImage[imgX][imgY][0])[-1]))
            else:
                lenBin += str(bin(self.hostImage[imgX][imgY][0])[-1])

            index += 1
        dataToDecode = (np.packbits(np.array(dataToDecode),bitorder="big"))

        if(verbose):
            print(dataToDecode)
        dataToDecode.tofile(outFile)

#Handles argparse in main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A program to hide data in images.", epilog="Example: \n./lsb.py encode hostImage.png encodeData.txt")

    parser.add_argument("operation", help="The desired operation: encode/decode")
    parser.add_argument("host", help="Image")
    parser.add_argument("data", help="File to encode/Name of decoded file")
    parser.add_argument("-c","--copy", help="Specifies output handle for host image. Overwrites host if not set")
    parser.add_argument("-f","--force",help="Override all verification prompts",action="store_true")
    parser.add_argument("-v","--verbose",help="Prints decoded data (Recommended for text only)",action="store_true")
    parser.add_argument("-t","--text",help="Handles the input file as text",action="store_true")

    args = parser.parse_args()
    host = frame()
    host.openHost(args.host)
    
    if(args.operation.lower() == "encode"):

        host.openFile(args.data,parseText=args.text)
        hostHandle = args.copy if args.copy else args.host

        if(hostHandle == args.host):
            if(args.force):
                prompt = "yes"
            else:
                prompt = input("This will overwrite host image (unless lossy): " + args.host + " \nDo you want to continue? (yes/no):\n").lower()
            if(prompt == "yes"):
                host.encodeImg(handle=hostHandle)
            elif(prompt == "no"):
                print("Terminating...")
            else:
                print("Unknown input. Terminating...")
        else:
            host.encodeImg(handle=hostHandle)

    elif(args.operation.lower() == "decode"):
        host.decodeImg(outFile=args.data, verbose=args.verbose)
    
    else:
        print("Unknown operation. Supported operations are: Encode/Decode")