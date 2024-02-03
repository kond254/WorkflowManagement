import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DialogComponent } from '../app/dialog/dialog.component';

@Injectable({
  providedIn: 'root',
})
export class DialogService {
  constructor(private dialog: MatDialog) {}

  openDialog(title: string, message: string): void {
    this.dialog.open(DialogComponent, {
      width: '250px',
      data: { title, message },
    });
  }
}
