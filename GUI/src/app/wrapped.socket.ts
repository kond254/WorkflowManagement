import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Injectable({
  providedIn: 'root',
})
export class WrappedSocket extends Socket {
  constructor() {
    super({ url: 'http://127.0.0.1:5000', options: {} });
  }
}
