

//version compiler
pragma solidity ^0.4.11;
contract mdcoin_ico {

    // Intrducing the  maximum no of mdcoins will be sale
    uint256 public max_mdcoins = 10000000 ;

    //Intrducing the usd  to mdcoins
     uint256 public usd_to_mdcoins  = 1000;

     //Intrducing the total no  of addcoins brought by invester
     uint public total_mdcoins_brought  = 0;

     //mapping from invester address
     mapping(address => uint) equity_mdcoins;
     mapping(address => uint) equity_usd;
     //checking if an invester can buy hadcoins
     modifier can_buy_mdcoin(uint usd_invested){
         require (usd_invested*usd_to_mdcoins + total_mdcoins_brought <= max_mdcoins);
         _;
     }
     //Getting the equity in hadcoins
     function  equity_in_mdcoin(address investor) external constant returns(uint){
         return  equity_mdcoins[investor];

     }
         function  equity_in_usd(address investor) external constant returns(uint){
         return  equity_usd[investor];

}
         function buy_mdcoins(address investor ,uint usd_invested ) external
          can_buy_mdcoin( usd_invested){
               uint mdcoins_bought = usd_invested * usd_to_mdcoins;
                equity_mdcoins[investor] += mdcoins_bought;
                equity_usd[investor] = equity_mdcoins[investor]/1000;
                total_mdcoins_brought += mdcoins_bought;

          }
           function sell_mdcoins(address investor ,uint mdcoins_sold ) external{


                equity_mdcoins[investor] -= mdcoins_sold;
                equity_usd[investor] = equity_mdcoins[investor]/1000;
                total_mdcoins_brought -= mdcoins_sold;

}
}
