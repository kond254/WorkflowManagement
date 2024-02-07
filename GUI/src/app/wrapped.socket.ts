import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Injectable({
  providedIn: 'root',
})

//This class is an extension of the class SocketService in socket.service.ts and is used to set the socket configuration, here the specified URL server address.  
export class WrappedSocket extends Socket {
  constructor() {
    super({ url: 'http://141.26.157.71:5000', options: {} });
  }
}