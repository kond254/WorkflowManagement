import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})

// Klasse ermöglicht einen boolean Wert zwischen Componenten auszutauschen (Login)
export class LoginService {
  private isLoggedIn: boolean = false;

  getloginValue(): boolean {
    return this.isLoggedIn;
  }

  setloginValue(value: boolean): void {
    this.isLoggedIn = value;
  }
}