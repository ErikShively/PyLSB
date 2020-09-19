# PyLSB
A program to hide data in images.
## Usage
`lsb.py [-h] [-c COPY] [-f] [-v] [-t] operation host data`

Example:
`./lsb.py encode hostImage.png encodeData.txt`


| Positional Arguments | Description |
| --- | --- |
| operation | The desired operation: encode/decode |
| host | Image |
| data | File to encode/Name of decoded file |

| Optional Arguments | Description |
| --- | --- |
| -h, --help | Show a help message and exit |
| -c COPY, --copy COPY | Specifies output handle for host image. Overwrites host if not set  |
| -f, --force | Override all verification prompts |
| -v, --verbose | Prints decoded data (Recommended for text only) |
| -t, --text | Handles the input file as text |

## Methods

`openFile(fileHandle, [parseText], [encoding])`

Opens a file to encode into the host image

| Parameters | Description |
| --- | --- |
| fileHandle | The path of the file to open |
| parseText, default=False | Bool to determine whether to process the file as text |
| encoding, default="utf-8" | The encoding of the text, provided praseText is True |
        
| Returns | Description |
| --- | --- |
| Success | A bool indicating if the operation was performed successfully |

`openHost(ImgHandle)`

Opens a host image

| Parameters | Description |
| --- | --- |
| imgHandle | Path of file to open |

| Returns | Description |
| --- | --- |
| None | This function modifies the object and returns nothing. |

`encodeImg([handle])`
Encodes data to host. Takes the output image handle. Returns True if successful.

| Parameters | Description |
| --- | --- |
| Handle, default = "output.png" | File path for data |

| Returns | Description |
| --- | --- |
| Successful | Bool indicating if operation was successful |

`encodeImg([handle])`
Decodes image. Takes output handle, verbosity (see arguments). Returns true if successful.

| Parameters | Description |
| --- | --- |
| OutFile | The handle of the output file |
| Verbose | Bool to determine whether or not the output should be printed |

| Returns | Description |
| --- | --- |
| Successful | Bool indicating if operation was successful |
