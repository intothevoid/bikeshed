import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

interface Product {
  id: number;
  name: string;
  description: string;
  price: string;
  imageUrl: string;
  quantity: number;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  products: Product[] = [];

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService.sendGetRequest().subscribe((data: any) => {
      console.log(data);
      this.products = data;
    });
  }
}
