import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})

//This class is used to convert the entered password (clear text) from login into a hash, to compare this password hash input with the stored user password hash
export class HashService {

  //Function that can be called by other components to convert the entered password into SHA-256
  hashPassword(password: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);

    return crypto.subtle.digest('SHA-256', data).then((buffer) => {
      const hashArray = Array.from(new Uint8Array(buffer));
      const hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
      return hashHex;
    });
  }
}