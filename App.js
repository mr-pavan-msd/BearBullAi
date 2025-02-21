import React from "react";
import { View, Text, TouchableOpacity, ScrollView, TextInput, FlatList } from "react-native";

const gainers = ["Stock A", "Stock B", "Stock C"];
const losers = ["Stock X", "Stock Y", "Stock Z"];

const App = () => {
  return (
    <View className="flex-1 bg-black p-4">
      <ScrollView>
        {/* Header */}
        <View className="flex-row justify-between items-center">
          <Text className="text-white text-2xl font-bold italic">bear bull Ai</Text>
          <View className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
            <Text className="text-red-500 text-xs">search symbol</Text>
          </View>
        </View>

        {/* Search Bar */}
        <TextInput
          className="bg-gray-800 text-white p-2 my-4 rounded"
          placeholder="Search for a stock..."
          placeholderTextColor="#ccc"
        />

        {/* Scrollable Indexes */}
        <View className="bg-gray-400 p-3 my-4 rounded">
          <Text className="text-black text-lg font-bold italic text-center">scrollable indexes</Text>
        </View>

        {/* Buttons */}
        <View className="flex-row justify-between">
          <TouchableOpacity className="bg-teal-700 px-4 py-2 rounded" accessibilityLabel="Explore Stocks">
            <Text className="text-white italic">explorer button</Text>
          </TouchableOpacity>
          <TouchableOpacity className="bg-teal-700 px-4 py-2 rounded" accessibilityLabel="Popular Stocks">
            <Text className="text-white italic">popular stocks button</Text>
          </TouchableOpacity>
          <TouchableOpacity className="bg-teal-700 px-4 py-2 rounded" accessibilityLabel="Watchlist">
            <Text className="text-white italic">watch list button</Text>
          </TouchableOpacity>
        </View>

        {/* Top Searched Stocks */}
        <Text className="text-white text-lg font-bold mt-4">top searched stocks</Text>
        <View className="bg-gray-400 h-20 rounded my-2" />

        {/* Today's Gainers */}
        <Text className="text-white text-lg font-bold italic mt-4">Today's gainers</Text>
        <FlatList
          data={gainers}
          horizontal
          keyExtractor={(item) => item}
          renderItem={({ item }) => (
            <View className="bg-gray-400 w-20 h-20 rounded m-2 flex items-center justify-center">
              <Text className="text-black">{item}</Text>
            </View>
          )}
        />

        {/* Today's Losers */}
        <Text className="text-white text-lg font-bold italic mt-4">Today's losers</Text>
        <FlatList
          data={losers}
          horizontal
          keyExtractor={(item) => item}
          renderItem={({ item }) => (
            <View className="bg-gray-400 w-20 h-20 rounded m-2 flex items-center justify-center">
              <Text className="text-black">{item}</Text>
            </View>
          )}
        />
      </ScrollView>

      {/* Bottom Navigation */}
      <View className="absolute bottom-0 left-0 right-0 bg-gray-300 py-3 flex-row justify-around">
        <TouchableOpacity className="bg-red-500 p-3 rounded-full" accessibilityLabel="Home">
          <Text className="text-white">home</Text>
        </TouchableOpacity>
        <TouchableOpacity className="bg-red-500 p-3 rounded-full" accessibilityLabel="Dashboard">
          <Text className="text-white">dashboard</Text>
        </TouchableOpacity>
        <TouchableOpacity className="bg-red-500 p-3 rounded-full" accessibilityLabel="Stock Alerts">
          <Text className="text-white">stock alert</Text>
        </TouchableOpacity>
        <TouchableOpacity className="bg-red-500 p-3 rounded-full" accessibilityLabel="AI Chat Board">
          <Text className="text-white">ai chat board</Text>
        </TouchableOpacity>
        <TouchableOpacity className="bg-red-500 p-3 rounded-full" accessibilityLabel="Portfolio">
          <Text className="text-white">portfolio</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default App;
