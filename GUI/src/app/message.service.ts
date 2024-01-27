import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})

// Bekommt Daten vom HR Departemnt und wird hier gespeichert. 
export class DataMessageService {
  private candidates: any[] = [];

  saveData(newData: any): void {
    this.candidates.push(newData);
    console.log('Saved data locally.');
  }

  getDataNews(): any[] {
    return this.candidates;
  }
}
