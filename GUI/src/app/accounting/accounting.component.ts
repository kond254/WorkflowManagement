import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-accounting',
  templateUrl: './accounting.component.html',
  styleUrl: './accounting.component.css'
})
export class AccountingComponent implements OnInit {
  changeOrder() {
    throw new Error('Method not implemented.');
  }
  invoices = [
    { id: 'invoice1', amount: 100.00, pdfUrl: 'invoice1.pdf' },
    { id: 'invoice2', amount: 150.00, pdfUrl: 'invoice2.pdf' },
    // Weitere Rechnungen können hier hinzugefügt werden
  ];

  constructor() { }

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
}
