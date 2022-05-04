#include <iostream>
#include <vector>

using namespace std;

class Room{

public:
    Room(string TypeRoom_, double square_){
        TypeRoom = TypeRoom_,
                square = square_;
    }

    string TypeRoom;
    double square;

public:
    double GetSquareRoom(){
        return square;
    }
};

class Flat{

    double height;
    bool balcony;
    int floor;
    string address;
    string number;
    double price;
    string owner;
    vector<Room> rooms;

public:
    Flat(double height_, bool balcony_, int floor_, string address_,string number_, double price_, string owner_){
        height = height_;
        balcony = balcony_;
        floor = floor_;
        address = address_;
        number = number_;
        price = price_;
        owner = owner_;
    }

    string get_owner(){
        return owner;
    }
    void set_owner(string owner){
        this->owner = owner;
    }

    string getAddress(){
        return address;
    }

    void addRoomInFlat(double squareRoom, string TypeRoom){
        rooms.push_back(Room(TypeRoom, squareRoom));
        cout << "Room has been created" << endl;
    }

    double getSquareFlat(){
        double squareAllRooms = 0;
        for(int i = 0; i < rooms.size(); i++)
        {
            squareAllRooms += rooms[i].GetSquareRoom();
        }
        return squareAllRooms;
    }

    void getInfoAllRooms(int numberRoom)
    {
        if(numberRoom == -1)
        {
            for(int i = 0; i < rooms.size(); i++)
            {
                cout << "NAME ROOM: " << rooms[i].TypeRoom << endl;
                cout << "SQUARE ROOM: " << rooms[i].square << endl;
            }
        }
        else
        {
            cout << "NAME ROOM: " << rooms[numberRoom].TypeRoom << endl;
            cout << "SQUARE ROOM: " << rooms[numberRoom].square << endl;
        }
    }

    int getCountRooms(){
        return rooms.size();
    }

    double getPriceAllSquare()
    {
        double price;
        price = 0;
        for(int i = 0; i < rooms.size(); i++){
            double square = rooms[i].square;
            cout << square << endl;
            cout << rooms.size() << endl;
            price += 79100.0 * square;
            cout << price ;
        }
        return price;
    }

    double getHeight(){
        return height;
    }

    void setFloor(int floor){
        this->floor = floor;
    }

    void setAddress(string address){
        this->address = address;
    }

    int getFloor(){
        return floor;
    }

    double getPrice(){
        return price;
    }

    void setPrice(double price){
        this->price = price;
    }

    void getPassportFlat()
    {
        cout << "==========================================" << endl;
        cout << "==============P A S P O R T ==============" << endl;
        cout << "=========================================="<< endl;
        cout << "OWNER: " << get_owner() << endl;
        cout << "Square Flat: " << getSquareFlat() << "meters square"<< endl;
        cout << "Cost apartment: " << fixed << getPrice() << "rubles, " << "Rooms: " << getCountRooms() << endl;
        cout << "Height: " << getHeight() << "meters" << endl;
        cout << "Address: " << getAddress() << ", " << getFloor() << " floor" << endl;
        getInfoAllRooms(-1);
    }
};

int main()
{
    string answer;
    Flat flat(226.5, true, 11, "Yuria Tena, 10", "50", 0, "Nikita Dolbak");
    cout << "Do you want to launch the apartment configurator?" << endl;
    cout << "[Yes or No] -"; cin >> answer;
    if(answer == "Yes")
    {
        int n;
        cout << "Enter the number of rooms in your apartment" << endl;
        cout << "Enter: "; cin >> n;
        for(int i = 0; i < n; i++)
        {
            string nameRoom;
            double squareRoom;
            cout << "Enter the square of the room and the name of the room" << endl;
            cin >>squareRoom >> nameRoom;
            flat.addRoomInFlat(squareRoom, nameRoom);
        }
        cout << "I calculate prices per square meter. The price per square meter in your area is 79.100 rubles" << endl;
        cout << "Please wait." << endl;
        cout << "Please wait.." << endl;
        cout << "Please wait..." << endl;
        cout << "Since you have finished the apartment configuration, would you like to check what happened?" << endl;
        answer = "";
        cout << "[Yes or No]"; cin >> answer;
        double price;
        price = flat.getPriceAllSquare();
        flat.setPrice(price);
        if(answer == "Yes")
        {
            flat.getPassportFlat();
        }
        else
        {
            answer = "";
            cout << "Thanks for using our app. Rate from 1 to 5." << endl; cin >> answer;
            return 0;
        }
    }
#pragma region Otka3
    else
    {
        answer = "";
        cout << "Do you want to see information about the apartment?" << endl;
        cout << "[Yes or No] "; cin >> answer;
        if(answer == "Yes")
        {
            flat.getPassportFlat();
        }
        else
        {
            answer = "";
            cout << "Thanks for using our app. Rate from 1 to 5." << endl; cin >> answer;
            return 0;
        }
    }
#pragma endregion Otka3
}
