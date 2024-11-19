import numpy as np
import struct

def rice_encode(samples, k):
    """
    Encodes the input samples using Rice codes with parameter k.
    """
    encoded_bits = []
    
    for x in samples:
        abs_x = abs(x)
        sign_bit = 1 if x < 0 else 0
        q = abs_x >> k  # Quotient
        r = abs_x & ((1 << k) - 1)  # Remainder
        encoded_bits.extend([1] * q + [0])

        encoded_bits.extend([int(b) for b in f"{r:0{k}b}"])
       
        if abs_x > 0:
            encoded_bits.append(sign_bit)
    
    return encoded_bits

def rice_decode(encoded_bits, k):
    """
    Decodes the input bitstream using Rice codes with parameter k.
    """
    decoded_samples = []
    i = 0
    
    while i < len(encoded_bits):
        q = 0
        while encoded_bits[i] == 1:
            q += 1
            i += 1
        i += 1 # skip the 0 bit
        
        # Binary decoding for remainder
        r = int("".join(map(str, encoded_bits[i:i+k])), 2)
        i += k
        
        abs_x = (q << k) + r
        if abs_x > 0:
            sign_bit = encoded_bits[i]
            i += 1
            x = -abs_x if sign_bit else abs_x
        else:
            x = 0
        
        decoded_samples.append(x)
    
    return decoded_samples

def main():
    # 1. Read the audio file
    input_file = "Queen_sint8.raw"
    with open(input_file, "rb") as f:
        raw_data = f.read()
    
    samples = np.frombuffer(raw_data, dtype=np.int8)  

    # 2. Rice encoding
    k = 4  
    encoded_bits = rice_encode(samples, k)

    # 3. Rice decoding
    decoded_samples = rice_decode(encoded_bits, k)

    # 4. Validation
    if np.array_equal(samples, decoded_samples):
        print("Success: Original and decoded data match.")
    else:
        print("Error: Data mismatch.")

    # 5. Measure bitstream size
    bitstream_size = len(encoded_bits)
    print(f"Rice Parameter (k = {k}) Bitstream Size: {bitstream_size} bits")
    
    # Optional: Save encoded bits to a file
    encoded_file = "encoded_rice.bin"
    with open(encoded_file, "wb") as f:
        encoded_bytes = np.packbits(encoded_bits, bitorder='big')
        f.write(encoded_bytes)
    print(f"Encoded bitstream saved to {encoded_file}")

if __name__ == "__main__":
    main()
