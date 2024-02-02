import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class HashService {
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