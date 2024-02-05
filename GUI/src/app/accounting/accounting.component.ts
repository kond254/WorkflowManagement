import { Component, OnInit } from '@angular/core';
import { DialogService } from '../dialog.service';

@Component({
  selector: 'app-accounting',
  templateUrl: './accounting.component.html',
  styleUrls: ['./accounting.component.css']
})

export class AccountingComponent implements OnInit {
  jobtitle:string ='';
  id:string = '';
  newEmployeesAmount: number = 0;
  sum:number = 0;
  result:number = 0;
  step = 0;
  dataNews: any[] = [];

  constructor(private dialogService: DialogService) {}

  // constructor(private dataService: DataService) {
  //   this.updateData();
  // }


  // Funktion setzt die Nummer der Pannel, für die Funktion Zurück/Vor
  setStep(index: number) {
    this.step = index;
  }

  nextStep() {
    this.step++;
  }

  prevStep() {
    this.step--;
  }

  // Initialisieren Sie das candidates-Array mit den Daten aus der JSON-Datei
 

  //Funktion speichert die Benutzer eingaben
  // saveData(): void {
  //   const newData = {
  //     jobtitle: this.jobtitle,
  //     number: this.number,
  //     location: this.location,
  //     salary: this.salary,
  //     additionalinformation: this.additionalinformation,
  //   };

  //   // hier neuen Daten in Array
  //   this.jobinformation.push(newData);
  //   console.log('Saved data local.');

  //   this.jobtitle = '';
  //   this.number = '';
  //   this.location = '';
  //   this.salary = 0;
  //   this.additionalinformation = '';
  // }


  // Funktion, um den Job zu akzeptieren
  acceptPayment(item: any): void {
    // hier die Logik zum Akzeptieren des Jobs implmentieren
    console.log('Payment accepted:', item);
  }

  // Funktion, um den Job abzulehnen
  rejectPayment(item: any): void {
    // hier die Logik zum Ablehnen des Jobs des Jobs implmentieren
    console.log('Payment rejected:', item);
  }

  // Funktion übergibt den Array datahrdepartment news von message.service.ts
  // updateData() {
  //   this.dataNews = this.dataService.getDataNews();
  // }

  invoices = [
    { id: 'invoice1', amount: 100.00, pdfUrl: 'invoice1.pdf' },
    { id: 'invoice2', amount: 150.00, pdfUrl: 'invoice2.pdf' },
    // Weitere Rechnungen können hier hinzugefügt werden
  ];

  ngOnInit(): void {
  }

  showPDF(pdfUrl: string): void {
    // Hier implementierst du die Logik zum Anzeigen des PDF-Dokuments
    alert('PDF anzeigen: ' + pdfUrl);
  }

  acceptInvoice(invoiceId: string): void {
    // Hier implementierst du die Logik zum Akzeptieren der Rechnung
    alert('Rechnung akzeptieren: ' + invoiceId);
  }

  claimInvoice(invoiceId: string): void {
    // Hier implementierst du die Logik zum Reklamieren der Rechnung
    alert('Rechnung reklamieren: ' + invoiceId);
  }

  changeOrder(): void {
    this.invoices.reverse();
  }

 
  //Funktion für Dialog Popup Pay
  openDialogPay(): void {
    this.dialogService.openDialog('Invoice', 'Are you sure to pay the invoices?');
  }

  //Funktion für Dialog Popup Reject
  openDialogReject(): void {
    this.dialogService.openDialog('Invoice', 'Are you sure to reject the invoices?');
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
