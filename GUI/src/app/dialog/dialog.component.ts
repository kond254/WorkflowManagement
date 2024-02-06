import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-dialog',
  templateUrl: './dialog.component.html',
  styleUrl: './dialog.component.css'
})

//This class contains a constructor that uses the MatDialogRef instance and the MAT_DIALOG_DATA injection. The MatDialogRef makes it possible to control the dialog window, while MAT_DIALOG_DATA can transfer data to the dialog.
export class DialogComponent {

  constructor(
    public dialogRef: MatDialogRef<DialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  //This method closes the dialogue window when corresponding actions are performed by the user
  onClose(): void {
    this.dialogRef.close();
  }

}
