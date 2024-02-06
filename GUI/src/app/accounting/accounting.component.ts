import { Component, OnInit } from '@angular/core';
import { DataServiceInterface } from '../data.service';


//This interface defines the structure of the invoices Object
interface Invoice{
  ProcessID: number;
  numberOfPosition: number;
  compensation: number;
  sumPay: number;
}

@Component({
  selector: 'app-accounting',
  templateUrl: './accounting.component.html',
  styleUrls: ['./accounting.component.css']
})

export class AccountingComponent implements OnInit {

  constructor(private dataServiceInterface: DataServiceInterface) {}

  step = 0;
  dataInvoice: Invoice[]=[];

  // In this method, various functions are called to load data.
  async ngOnInit(): Promise<any> {
    await this.getInvoices();
  }

  // The getInvoices() method retrieves the invoices from DataServiceInterface
  async getInvoices() {
    this.dataServiceInterface.getInvoices().subscribe(
      data => {
        this.dataInvoice = data as Invoice[];
        console.log("Data invoices retrieved");
        console.log(this.dataInvoice);
      },
      error => {
        console.error("Error fetching job offer data:", error);
      }
    );
  }

  // Funktion setzt die Nummer des Pannels, für die Funktion Zurück/Vor
  setStepInvoice(index: number) {
    this.step = index;
  }
  nextStepInvoice() {
    this.step++;
  }
  prevStepInvoice() {
    this.step--;
  }

}
